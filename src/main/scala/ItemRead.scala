import org.apache.spark.{SparkConf, SparkContext}

import scala.collection.mutable.ArrayBuffer
import com.easou.dingjing.library.{ItemInfo, ReadEvent}

object ItemRead {
  def main(args: Array[String]): Unit = {
    if (args.length < 3) {
      println("请输入：物品信息、阅读事件日志、保存路径")
      sys.exit(-1)
    }

    val iteminfoPath = args(0)
    val readeventPath = args(1)
    val savePath = args(2)

    val conf = new SparkConf()
      .setAppName("item_read")
      .set("spark.executor.memory", "20g")
      .set("spark.driver.memory", "6g")
      .set("spark.cores.max", "30")
      .set("spark.dynamicAllocation.enabled", "false")
      .setMaster("local[50]")
    //      .setMaster("spark://qd01-tech2-spark001:7077,qd01-tech2-spark002:7077")
    val sc = new SparkContext(conf)

    // 获取物品信息并解析
    val iteminfoRDD = sc.textFile(iteminfoPath).flatMap(x => {
      val buffer = new ArrayBuffer[Tuple2[String,
        Tuple10[String, String, String, String, String, String, String, String, String, String]]]()
      val it = new ItemInfo().parseLine(x)
        .getValues(List("name", "author", "mask_level", "fee_flag", "ncp", "by", "tf", "fc", "ii", "ci"))
      val gid = it.head
      val name = it(1)
      val author = it(2)
      val masklevel = it(3)
      val feeflag = it(4)
      val ncp = it(5)
      val by = it(6)                                   // 包月
      val tf = it(7)                                   // 限免
      val fc = it(8)                                   // 免费 cp
      val ii = it(9)                                   // 互联网
      val ci = it(10)                                  // 按章计费
      // 一条变两条，分别是 宜搜、微卷
      val maskFlag = this.datastreamCheck(masklevel)
      val byFlag = this.datastreamCheck(by)
      val tfFlag = this.datastreamCheck(tf)
      val fcFlag = this.datastreamCheck(fc)
      val iiFlag = this.datastreamCheck(ii)
      val ciFlag = this.datastreamCheck(ci)
      var cpstr = ""
      if (cpName.contains(ncp)) {
        cpstr = cpName(ncp)
      } else {
        cpstr = ncp
      }

      buffer.append((gid + "_easou", (name, author, cpstr,
        maskFlag._1, feeflag, byFlag._1, tfFlag._1, fcFlag._1, iiFlag._1, ciFlag._1)))
      buffer.append((gid + "_weijuan", (name, author, cpstr,
        maskFlag._2, feeflag, byFlag._2, tfFlag._2, fcFlag._2, iiFlag._2, ciFlag._2)))

      for (i <- buffer.toList)
        yield i
    })

    // 解析阅读日志，获取阅读日志信息
    val readeventRDD = sc.textFile(readeventPath).map(x => {
      var gidFlag = ""
      val rd = new ReadEvent().parseLine(x)
        .getValues(List("uid", "appudid", "sort", "usertype", "booktype", "gid", "entrance", "appid"))
      val uid = rd(0)
      val appudid = rd(1)
      val sort = rd(2)
      val userType = rd(3)
      val bookType = rd(4)
      val gid = rd(5)
      val entrance = rd(6)
      val appid = rd(7)

      val appFlag = this.getAppflagByAppid(appid)
      if (gid != "") {
        gidFlag = gid + "_" + appFlag
      }
      if ("书架" != entrance) {
        gidFlag = ""
      }
      (gidFlag, List((appudid, strToInt(sort).toString, userType, bookType)))
    }).filter(x => x._1 != "").reduceByKey(_:::_)

    /**
     * 合并物品信息 + 日志
     * 物品：(gid + "_easou", (name, author, cp, maskFlag, fee_flag, by, tf, fc, ii, ci)
     * 阅读：(gid + "_easou", (appudid, sort, userType, bookType))
     */
    val readinfoRDD = readeventRDD.join(iteminfoRDD)
    val resultRDD = readinfoRDD.map(x => {
      val gidFlag = x._1
      val readEvent = x._2._1
      val itemInfo = x._2._2

      val name = itemInfo._1
      val author = itemInfo._2
      val cp = itemInfo._3
      val mask = itemInfo._4
      val fee = itemInfo._5
      val by = itemInfo._6
      val tf = itemInfo._7
      val fc = itemInfo._8
      val ii = itemInfo._9
      val ci = itemInfo._10

      val iteminfoStr = name + "\t" + author + "\t" + cp + "\t" + mask + "\t" + fee + "\t" +
                        by + "\t" + tf + "\t" + fc + "\t" + ii + "\t" + ci

      // 非包月书
      var userNum = 0
      var chapterNum = 0
      val appudidSet = scala.collection.mutable.Set[String]()
      val chapterSet = scala.collection.mutable.Set[String]()

      // 包月书 - 包月用户
      var bysByuUserNum = 0
      var bysByuChapterNum = 0
      val bysByuAppudidSet = scala.collection.mutable.Set[String]()
      val bysByuChapterDict = scala.collection.mutable.Set[String]()

      // 包月书 - 非包月用户
      var bysFByuUserNum = 0
      var bysFByuChapterNum = 0
      val bysFByuAppudidSet = scala.collection.mutable.Set[String]()
      val bysFByuChapterDict = scala.collection.mutable.Set[String]()

      for (i <- readEvent) {
        //appudid strToInt(sort).toString userType bookType
        val appudid = i._1
        val sort = i._2
        val userType = i._3
        val bookType = i._4
        if (by.toInt == 1) {
          if ("包月" == userType) {
            // 包月用户 + 包月书
            bysByuAppudidSet.add(appudid)
            bysByuChapterDict.add(sort + "|" + appudid)
          } else {
            // 非包月用户 + 包月书
            bysFByuAppudidSet.add(appudid)
            bysFByuChapterDict.add(sort + "|" + appudid)
          }
        } else {
          appudidSet.add(appudid)
          chapterSet.add(sort + "|" + appudid)
        }
      }
      // 统计结果
      bysByuUserNum = bysByuAppudidSet.toList.length
      bysFByuUserNum = bysFByuAppudidSet.toList.length

      bysByuChapterNum = bysByuChapterDict.toList.length
      bysFByuChapterNum = bysFByuChapterDict.toList.length

      // 非包月书统计
      userNum = appudidSet.toList.length
      chapterNum = chapterSet.toList.length

      gidFlag + "\t" + iteminfoStr + "\t" + userNum.toString + "\t" + chapterNum.toString + "\t" +
        bysByuUserNum.toString + "\t" + bysByuChapterNum.toString + "\t" +
        bysFByuUserNum.toString + "\t" + bysFByuChapterNum.toString
    })

    resultRDD.filter(_ != "").repartition(1).saveAsTextFile(savePath)
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
  // 根据 appid 获取标记
  def getAppflagByAppid(appid: String): String = {
    var flag = ""

    if(appidName.contains(appid)) {
      flag = appidName(appid)
    }
    flag
  }

  // 判断 宜搜是否屏蔽？ 判断微卷是否屏蔽？
  def datastreamCheck(str: String): Tuple2[String, String] = {
    val arr = str.split(",")
    var easou = "0"
    var weijuan = "0"

    if (arr.length >= 2) {
      val estr = arr(0)
      val wstr = arr(1)
      for (i <- estr.toList) {
        if (i.toInt >= 1) {
          easou = "1"
        }
      }
      for (j <- wstr.toList) {
        if (j.toInt >= 1) {
          weijuan = "1"
        }
      }
    }

    (easou, weijuan)
  }

  val appidName = scala.collection.immutable.Map[String, String] (
    "10001" -> "easou",
    "20001" -> "weijuan"
  )
  // ncp id 和 名字对应
  val cpName = scala.collection.immutable.Map[String, String] (
    "0"  -> "免费书",
    "1"  -> "盛大",
    "6"  -> "纵横",
    "8"  -> "掌阅",
    "9"  -> "3G书城",
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
    "100"-> "大唐中文网",
    "101"-> "安夏书院",
    "102"-> "触阅文化传媒",
    "103"-> "恋小说",
    "104"-> "星汇传媒",
    "105"-> "雁北堂",
    "106"-> "中文在线",
    "107"-> "北京红阅科技",
    "108"-> "磨铁中文网",
    "109"-> "书影阅读",
    "110"-> "四喜文学",
    "111"-> "飞扬文学网",
    "1000012"-> "2000000035",
    "1000002"-> "云起",
    "1000001"-> "阅文",
    "1056029"-> "小说阅读网",
    "1047626"-> "潇湘书院",
    "1000023"-> "红袖添香",
    "1000024"-> "言情小说吧",
    "1000003"-> "起点女生", 
    "1000009"-> "起点文学网",
    "1000005"-> "起点男生"
  )
}
