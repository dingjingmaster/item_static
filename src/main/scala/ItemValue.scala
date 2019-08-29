import java.text.SimpleDateFormat
import java.util.Calendar

import ItemRead.cpName
import com.easou.dingjing.library.{ItemInfo, ReadEvent}
import org.apache.spark.{SparkConf, SparkContext}
import org.apache.spark.storage.StorageLevel

import scala.collection.mutable.ArrayBuffer

object ItemValue {

  val freeValue = 0.0025
  val chargeValue = 0.0225

  def main(args: Array[String]): Unit = {
    if (args.length < 5) {
      println("请输入：物品信息、bi阅读日志、今天时间戳、天数、保存路径")
      sys.exit(-1)
    }

    val iteminfoPath = args(0)
    val readEventPath = args(1)
    val today = args(2)
    val days = args(3)
    val savePath = args(4)

    val conf = new SparkConf()
      .setAppName("item_value")
      .set("spark.executor.memory", "20g")
      .set("spark.driver.memory", "6g")
      .set("spark.cores.max", "30")
      .set("spark.dynamicAllocation.enabled", "false")
      //      .setMaster("local[50]")
      .setMaster("spark://qd01-tech2-spark001:7077,qd01-tech2-spark002:7077")
    val sc = new SparkContext(conf)
    var readEventRDD = sc.parallelize(Seq[Tuple2[String, List[String]]]())

    // 获取物品信息并解析
    val iteminfoRDD = sc.textFile(iteminfoPath).map(x => {
      val it = new ItemInfo().parseLine(x)
        .getValues(List("name", "author", "mask_level", "fee_flag", "ncp", "by", "tf", "fc", "ii", "ci"))
      val gid = it.head
      val name = it(1)
      val author = it(2)
//      val masklevel = it(3)
//      val feeflag = it(4)
      val ncp = it(5)
      var cpStr = ""
      if (cpName.contains(ncp)) {
        cpStr = cpName(ncp)
      } else {
        cpStr = ncp
      }
      (gid, name + "\t" + author + "\t" + cpStr)
    })

    // 解析阅读日志，获取阅读日志信息
    for (p <- get_path(readEventPath, today, days.toInt)) {
      val readeventRDDt = sc.textFile(p).filter(_ != "").map(x => {
        /* 输出维度 */
        var gidO = ""
        var appidO = ""
        var userIdO = ""
        var chapterIdO = ""
        var chapterTypeO = ""
        val rd = new ReadEvent().parseLine(x)
          .getValues(List("uid", "appudid", "sort", "usertype", "booktype", "gid", "appid", "ischapterincharged", "userarea"))
        val uid = rd(0)
        val appudid = rd(1)
        val sort = rd(2)
        val userType = rd(3)
        /* 包月 */
        val bookType = rd(4)
        /* 包月 */
        val gid = "i_" + rd(5)
        val appid = rd(6)
        val isChapterCharge = rd(7)
        val userLevel = rd(8)

        if ("" != uid && "-1" != uid && "0" != uid) {
          userIdO = uid
        } else {
          userIdO = appudid
        }
        if ((gid != "i_") && (gid != "i_0")) {
          gidO = gid
        }

        if ("" != appid) {
          appidO = appid
        } else {
          appidO = "10001"
        }

        // 滤去漫画书的阅读量
        if (this.strToInt(rd(5)) >= 200000000) {      // 漫画
          appidO = "20001_1"
        }

        chapterIdO = sort
        if ("" != isChapterCharge) {
          chapterTypeO = isChapterCharge
          if ("no" == chapterTypeO.toLowerCase) {
            chapterTypeO = "免费(免费cp)"
          } else if ("yes" == chapterTypeO.toLowerCase) {
            chapterTypeO = "付费"
          }
        } else if ("免费互联网书" == bookType) {
          chapterTypeO = "互联网"
        } else {
          // 赠书、断更 合并到免费cp
          chapterTypeO = "免费(免费cp)"
        }
        // 修改免费名字
        if ("免费" == chapterTypeO) {
          chapterTypeO = "免费(免费cp)"
        }
        if (("免费CP书" == bookType) || ("赠书" == bookType) || ("断更" == bookType)) {
          chapterTypeO = "免费(免费cp)"
        }
        /* 非付费阅读 */
        // 按章计费 付费节点前 免费读
        if (("按章计费" == bookType) && ("免费(免费cp)" == chapterTypeO)) {
          chapterTypeO = "免费(按章计费)"
        }
        // 包月书免费读
        if (("包月" == bookType) && ("免费(免费cp)" == chapterTypeO)) {
          chapterTypeO = "免费(包月书)"
        }
        // 包月用户读包月书
        if (("包月" == userType) && ("包月" == bookType)) {
          chapterTypeO = "包月"
        }

        // 最后整合
        if (chapterTypeO == "付费" || chapterTypeO == "包月") {
          chapterTypeO = "付费"
        } else {
          chapterTypeO = "免费"
        }

        (gidO + "\t" + appidO + "\t" + chapterTypeO, Array[String](userIdO + "\t" + strToInt(chapterIdO).toString).toList)
      }).filter(x => x._1 != "" && x._2.nonEmpty)
      readEventRDD = readEventRDD.union(readeventRDDt)
    }

    val itemValueRDD = readEventRDD.reduceByKey(_:::_).map(x => (x._1, x._2.length)).map(x=> {
      val arr = x._1.split("\t")
      val gid = arr(0)
      val appid = arr(1)
      val chapter = arr(2)
      var c: Double = x._2.toDouble
      if (chapter == "付费") {
        c *= chargeValue
      } else {
        c *= freeValue
      }
      (gid + "\t" + appid, c)
    }).reduceByKey(_+_)

    // 保存结果
    itemValueRDD.map(x=>{
      val arr = x._1.split("\t")
      (arr.head, arr(1) + "\t" + arr(2))
    }).join(iteminfoRDD).map(x=>x._1 + "\t" + x._2._1 + "\t" + x._2._2)
      .repartition(1).saveAsTextFile(savePath)
  }

  def strToInt(str: String): Int = {
    var a: Int = 0
    try {
      a = str.toInt
    } catch {
      case _: Exception =>
    }
    a
  }

  def datastreamCheck(str: String): Tuple2[String, String] = {
    val arr = str.split(",")
    var easou = "0"
    var weijuan = "0"

    if (arr.length >= 2) {
      val estr = arr(0)
      val wstr = arr(1)
      for (i <- estr.toList) {
        if (i.toString.toInt >= 1) {
          easou = "1"
        }
      }
      for (j <- wstr.toList) {
        if (j.toString.toInt >= 1) {
          weijuan = "1"
        }
      }
    }

    (easou, weijuan)
  }

  def get_path(base: String, time: String, days: Int): Array[String] = {
    var tp = ""
    val arr = new ArrayBuffer[String]()
    val datastrparse = new SimpleDateFormat("yyyy-MM-dd")
    val dt = datastrparse.parse(time)
    val ca = Calendar.getInstance()
    ca.setTime(dt)
    for (i <- 0 until days) {
      tp = datastrparse.format(ca.getTime)
      arr.append(base + tp + "/")
      ca.add(Calendar.DAY_OF_MONTH, -1)
    }
    arr.toArray
  }
}
