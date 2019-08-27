import com.easou.dingjing.library.{ItemInfo, ReadEvent}
import org.apache.spark.storage.StorageLevel
import org.apache.spark.{SparkConf, SparkContext}

import scala.collection.mutable
import scala.collection.mutable.ArrayBuffer

object ItemRead {
  // ncp id 和 名字对应
  val cpName = scala.collection.immutable.Map[String, String](
    "0" -> "互联网书",
    "1" -> "盛大",
    "6" -> "纵横",
    "8" -> "掌阅",
    "9" -> "3G书城",
    "10" -> "书海",
    "11" -> "畅读",
    "12" -> "逐浪",
    "13" -> "凤栖梧小说网",
    "14" -> "九库文学",
    "15" -> "一千零一页",
    "17" -> "云阅文学",
    "18" -> "品阅",
    "19" -> "绝版中文网",
    "20" -> "大麦中金",
    "21" -> "哎呦互娱",
    "22" -> "阅明中文网",
    "24" -> "阅路小说网",
    "25" -> "酷匠网",
    "26" -> "咪咕阅读",
    "27" -> "永正",
    "28" -> "纸尚",
    "29" -> "万众中文网",
    "30" -> "凤凰书城",
    "31" -> "果维文化",
    "33" -> "网易云阅读",
    "34" -> "点众",
    "44" -> "景象文学",
    "45" -> "趣阅小说网",
    "46" -> "蔷薇书院",
    "47" -> "米汤中文网",
    "48" -> "神起中文网",
    "49" -> "锦瑟文学",
    "50" -> "书香文府",
    "51" -> "丹鼎四海",
    "52" -> "聚点艺盛",
    "54" -> "鼎甜科技",
    "55" -> "原创书殿",
    "56" -> "塔读",
    "57" -> "逸云书院",
    "58" -> "悦客中文网",
    "59" -> "落尘文学",
    "60" -> "作客文学网",
    "61" -> "凤鸣轩",
    "62" -> "幻想工场",
    "63" -> "文博",
    "64" -> "恺兴",
    "65" -> "创酷中文网",
    "66" -> "龙阅读",
    "67" -> "青春说",
    "68" -> "鬼姐姐",
    "69" -> "大鱼中文网",
    "70" -> "奇文阅读",
    "71" -> "艾月乐美",
    "72" -> "藤痕书院",
    "73" -> "天阅书城",
    "74" -> "幻想中文网",
    "75" -> "圣诞文学网",
    "76" -> "不可能的世界",
    "77" -> "青果阅读",
    "78" -> "玄娱中文网",
    "79" -> "有乐中文网",
    "80" -> "寒武纪年原创网",
    "81" -> "起创文学",
    "82" -> "四月天",
    "83" -> "0度小说",
    "84" -> "黑岩阅读",
    "85" -> "天下书盟",
    "86" -> "古阅读",
    "87" -> "老虎发威",
    "88" -> "风起中文网",
    "89" -> "恒言中文网",
    "90" -> "书丛网",
    "91" -> "长江中文网",
    "92" -> "华夏天空",
    "93" -> "豆读言情",
    "94" -> "阅书中文网",
    "95" -> "中天和信",
    "96" -> "公版书籍",
    "97" -> "梧桐中文",
    "98" -> "起承中文网",
    "99" -> "品阅文学网",
    "100" -> "大唐中文网",
    "101" -> "安夏书院",
    "102" -> "触阅文化传媒",
    "103" -> "恋小说",
    "104" -> "星汇传媒",
    "105" -> "雁北堂",
    "106" -> "中文在线",
    "107" -> "北京红阅科技",
    "108" -> "磨铁中文网",
    "109" -> "书影阅读",
    "110" -> "四喜文学",
    "111" -> "飞扬文学网",
    "1000012" -> "2000000035",
    "1000002" -> "云起",
    "1000001" -> "阅文",
    "1056029" -> "小说阅读网",
    "1047626" -> "潇湘书院",
    "1000023" -> "红袖添香",
    "1000024" -> "言情小说吧",
    "1000003" -> "起点女生",
    "1000009" -> "起点文学网",
    "1000005" -> "起点男生"
  )

  val appKeyMap = scala.collection.immutable.Map[String, String](
    "307A5C626E6C2F6472636E6E6A2F736460656473"-> "10001",    // Android 宜搜小说
    "307A5C626E6C2F69766472636E6E6A2F736460656473" -> "10001",        // Android 宜搜小说海外版
    "337A5C626E6C2F6472636E6E6A2F736460656473" -> "10001",            // ios 宜搜小说
    "337A5C626E6C2F6460726E742F7160656472636E6E6A" -> "10001",        // i-pad 宜搜小说
    "307A5C626F2F76646B74606F2F736460656473" -> "20001",              // Android 微卷（改为宜搜小说快读版）
    "307A5C626F2F76646B74606F2F6668736D" -> "20001",                  // Android 微卷女生（爱看小说）
    "307A5C626E6C2F6460726E742F736460656473" -> "10001",              // Android 宜搜电子书
    "307A5C626E6C2F6460726E742F6C606F697460" -> "",                   // Android 宜搜漫画
    "337A5C626E6C2F6569752F766B636E6E6A" -> "20001",                  // ios 微卷小说（快读小说阅读器）
    "337A5C626E6C2F6460726E742F6265636E6E6A" -> "",                   // ios 宜搜小说畅读版
    "307A5C626E6C2F7B6F6E77646D2F7978736460656473" -> "",             // Android 免费小说 txt
    "307A5C626E6C2F70636C676A6579722F736460656473" -> "",             // Android 全本免费小说
    "307A5C626E6C2F6C6770637B722F736460656473" -> "",                 // Android txt 免费全本追书
    "337A5C626E6C2F60686A606F2F60636E6E6A" -> "",                     // ios 爱看小说阅读器
    "337A5C626E6C2F76646B74606F2F6A6A606F" -> "",                     // ios 快看小说
    "307A5C76796C686F682F6460726E742F626E6C" -> "",                   // Android 微信小程序
    "337A5C6876796C686F682F6460726E742F626E6C" -> "",                 // ios 微信小程序
    "07A5C626F2F76646B74606F2F707468626A607171" -> "",                // Android 宜搜小说快读
    "307A5C626E6C2F7B6F6E77646D2F7978736460656473" -> "",             // 掌读txt免费小说
    "307A5C626E6C2F70636C676A6579722F736460656473" -> "",             // 全本免费快读小说
    "307A5C626E6C2F6C6770637B722F736460656473" -> ""                  // Android 全本快阅
  )

  def main(args: Array[String]): Unit = {
    if (args.length < 4) {
      println("请输入：物品信息、阅读事件日志、天阅读路径")
      sys.exit(-1)
    }

    val iteminfoPath = args(0)
    val readeventPath = args(1)
    val visitPath = args(2)
    val readSavePath = args(3)

    val conf = new SparkConf()
      .setAppName("item_read")
      .set("spark.executor.memory", "20g")
      .set("spark.driver.memory", "6g")
      .set("spark.cores.max", "30")
      .set("spark.dynamicAllocation.enabled", "false")
      //      .setMaster("local[50]")
      .setMaster("spark://qd01-tech2-spark001:7077,qd01-tech2-spark002:7077")
    val sc = new SparkContext(conf)

    // 获取物品信息并解析
    val iteminfoRDD = sc.textFile(iteminfoPath).flatMap(x => {
      val buffer = new ArrayBuffer[Tuple2[String, Tuple3[String, String, String]]]()
      val it = new ItemInfo().parseLine(x)
        .getValues(List("name", "author", "mask_level", "fee_flag", "ncp", "by", "tf", "fc", "ii", "ci"))
      val gid = it.head
      val name = it(1)
      val author = it(2)
      val masklevel = it(3)
      val feeflag = it(4)
      val ncp = it(5)
      var cpstr = ""
      if (cpName.contains(ncp)) {
        cpstr = cpName(ncp)
      } else {
        cpstr = ncp
      }
      buffer.append((gid + "{]10001", (name, author, cpstr)))
      buffer.append((gid + "{]20001", (name, author, cpstr)))
      for (i <- buffer.toList)
        yield i
    })

    // 解析阅读日志，获取阅读日志信息
    val readeventRDD = sc.textFile(readeventPath).filter(_ != "").map(x => {
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
        //        gidO = ""
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
      }else { // 赠书、断更 合并到免费cp
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
      // 互联网书
      if ("免费互联网书" == bookType) {
        chapterTypeO = "互联网"
      }
      (gidO, appidO, userIdO, strToInt(chapterIdO).toString, chapterTypeO, strToInt(userLevel).toString)
    }).filter(x => x._1 != "" && x._2 != "" && x._3 != "").persist(StorageLevel.MEMORY_AND_DISK) /* (gid, appid, 用户id, 章节序号, 章节类型) */

    val visitRDD = sc.textFile(visitPath).filter(_ != "").map(x => {
      var appkey = ""
      var phone_udid = ""
      val arr = x.split("\\x01", -1)
      if (arr.length >= 4) {
        appkey = arr(0)
        phone_udid = arr(3)
      }

      if (this.appKeyMap.contains(appkey)) {
        appkey = appKeyMap(appkey)
      }

      (appkey, phone_udid)
    }).filter(x => x._1 != "" || x._2 != "").persist(StorageLevel.MEMORY_AND_DISK)

    /* DAU */
    val easouDAU = visitRDD.filter(x => x._1 == "10001").map(_._2).distinct().count()
    val weijuanDAU = visitRDD.filter(x => x._1 == "20001").map(_._2).distinct().count()
    val manhuaDAU = 1

    /* 总 书籍量 */
    val easouItemAllNum = readeventRDD.filter(x => x._2 == "10001").map(x => x._1).distinct().count()
    val weijuanItemAllNum = readeventRDD.filter(x => x._2 == "20001").map(x => x._1).distinct().count()
    val manhuaItemAllNum = readeventRDD.filter(x => x._2 == "20001_1").map(x => x._1).distinct().count()

    /* 总 阅读量 */
    val easouUserAllNum = readeventRDD.filter(x => x._2 == "10001").map(x => x._3).distinct().count()
    val weijuanUserAllNum = readeventRDD.filter(x => x._2 == "20001").map(x => x._3).distinct().count()
    val manhuaUserAllNum = readeventRDD.filter(x => x._2 == "20001_1").map(x => x._3).distinct().count()

    /* 总 阅读章节数 */
    val easouChapterAllNum = readeventRDD.filter(x => x._2 == "10001").map(x =>x._1 + "|" + x._3 + "|" + x._4).distinct().count()
    val weijuanChapterAllNum = readeventRDD.filter(x => x._2 == "20001").map(x => x._1 + "|" + x._3 + "|" + x._4).distinct().count()
    val manhuaChapterAllNum = readeventRDD.filter(x => x._2 == "20001_1").map(x => x._1 + "|" + x._3 + "|" + x._4).distinct().count()

    /* 各类型书籍量 */
    val easouItemAll = readeventRDD.filter(x => x._2 == "10001").map(x => (x._5, List(x._1))).reduceByKey(_ ::: _).map(x => "easou_item\t" + x._1 + "\t" + x._2.toSet.toSeq.length.toString).collect().mkString("\n")
    val weijuanItemAll = readeventRDD.filter(x => x._2 == "20001").map(x => (x._5, List(x._1))).reduceByKey(_ ::: _).map(x => "weijuan_item\t" + x._1 + "\t" + x._2.toSet.toSeq.length.toString).collect().mkString("\n")

    /* 各类型用户量 */
    val easouUserAll = readeventRDD.filter(x => x._2 == "10001").map(x => (x._5, List(x._3))).reduceByKey(_ ::: _).map(x => "easou_user\t" + x._1 + "\t" + x._2.toSet.toSeq.length.toString).collect().mkString("\n")
    val weijuanUserAll = readeventRDD.filter(x => x._2 == "20001").map(x => (x._5, List(x._3))).reduceByKey(_ ::: _).map(x => "weijuan_user\t" + x._1 + "\t" + x._2.toSet.toSeq.length.toString).collect().mkString("\n")

    /* 各类型章节量 */
    val easouChapterAll = readeventRDD.filter(x => x._2 == "10001").map(x => (x._5, List(x._1 + x._4))).reduceByKey(_ ::: _).map(x => "easou_chapter\t" + x._1 + "\t" + x._2.toSet.toSeq.length.toString).collect().mkString("\n")
    val weijuanChapterAll = readeventRDD.filter(x => x._2 == "20001").map(x => (x._5, List(x._1 + x._4))).reduceByKey(_ ::: _).map(x => "weijuan_chapter\t" + x._1 + "\t" + x._2.toSet.toSeq.length.toString).collect().mkString("\n")

    /* 总的字段 */
    sc.parallelize(List[String](
      "easou_item" + "\t" + easouItemAllNum.toString + "\t"
        + "easou_user" + "\t" + easouUserAllNum.toString + "\t"
        + "easou_chapter" + "\t" + easouChapterAllNum.toString + "\n"
        + "weijuan_item" + "\t" + weijuanItemAllNum.toString + "\t"
        + "weijuan_user" + "\t" + weijuanUserAllNum.toString + "\t"
        + "weijuan_chapter" + "\t" + weijuanChapterAllNum.toString + "\n"
        + "manhua_item" + "\t" + manhuaItemAllNum.toString + "\t"
        + "manhua_user" + "\t" + manhuaUserAllNum.toString + "\t"
        + "manhua_chapter" + "\t" + manhuaChapterAllNum.toString,
      easouItemAll, weijuanItemAll,
      easouUserAll, weijuanUserAll,
      easouChapterAll, weijuanChapterAll,
      "easou_dau" + "\t" + easouDAU.toString + "\n"
      + "weijuan_dau" + "\t" + weijuanDAU.toString + "\n"
      + "manhua_dau" + "\t" + manhuaDAU.toString
    )).repartition(1).saveAsTextFile(readSavePath + "/summary")

    /* 基础数据准备 */
    /* gid_appid, name, author, cp, 付费X3, 限免X3, 免费X3, 包月X3, 互联网X3 */
    // (gidO, appidO, userIdO, strToInt(chapterIdO).toString, chapterTypeO, userLevel)
    val allDataRDDt = readeventRDD.map(x => (x._1 + "{]" + x._2, (x._3, x._4, x._5, x._6))).join(iteminfoRDD)
    val allDataRDD = allDataRDDt.map(x => {
      val gid = x._1          // gid{]appid
      val read = x._2._1
      val item = x._2._2

      val name = item._1
      val author = item._2
      val cp = item._3

      val userId = read._1
      val chapterId = read._2
      val chapterType = read._3
      val userLevel = read._4

      (gid, name, author, cp, userId, chapterId, chapterType, userLevel)
    }).persist(StorageLevel.MEMORY_AND_DISK)
    readeventRDD.unpersist(true)

    // 获取书籍用户地区
    val itemAreaRDD = allDataRDD.map(x => (x._1, Seq(x._8))).reduceByKey(_.toList:::_.toList).map(x => {
      val gid = x._1
      val area = x._2.toSet.toArray.filter(x => x != "0").sortBy(x => x.toInt).mkString(",")
      (gid, area)
    })

    // 获取阅读情况
    val allReadRDD = allDataRDD.map(x => (x._1 + "{]" + x._2 + "{]" + x._3 + "{]" + x._4 + "{]" + x._7, Seq((x._5, x._6))))
      .reduceByKey(_.toList:::_.toList).map(x => {
      val info = x._1.split("\\{\\]")
      val filter = new collection.mutable.ArrayBuffer[String]()
      for (i <- x._2) {
        filter.append(i._1 + "|" + i._2)
      }

      (info(0) + "{]" + info(1), (x._1, filter.toSet.toList.mkString("{]")))
    })

    // 整合阅读情况与书籍地区
    val readAreaRDD = allReadRDD.join(itemAreaRDD)
    readAreaRDD.map(x => {
      val gid = x._1
      val allRead = x._2._1
      val area = x._2._2

      allRead._1 + "{]" + area + "\t" + allRead._2
    }).filter(_ != "").repartition(1).saveAsTextFile(readSavePath + "/base_info/")
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
}
