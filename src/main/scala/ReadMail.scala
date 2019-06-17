import scala.collection.mutable.ArrayBuffer
import scala.io.Source

object ReadMail {
  def main(args: Array[String]): Unit = {
//    if (args.length < 2) {
//      println("请输入：日志路径 \t 输出结果路径")
//      sys.exit(-1)
//    }
//    val logPath = args(0)
//    val resultPath = args(1)

    val logPath = "./aa.txt"
    val resultPath = ""

    // 解析日志
    parseLog(logPath)




  }
  def parseLog(path: String) = {
    val file = Source.fromFile(path)
    for(line <- file.getLines()) {
      val arr = line.trim.split("\t")
      logList.append(arr.toList)
    }
  }

  def maskLevelList() = {
    var maskBookNum = 0
    var maskBookUserNum = 0
    var maskChargeChapterNum = 0

    var unmaskBookNum = 0
    var unmaskBookUserNum = 0
  }

  /**
    * gid, name, author, cp, mask, fee, by, tf, fc, ii, ci
    * userNum, chapterNum
    * bysByuUserNum, bysByuChapterNum
    * bysFByuUserNum, bysFBYuChapterNum
    */
  val logList = new ArrayBuffer[List[String]]()
  val maskLevel = new ArrayBuffer[Tuple7[String, Int, Double, Int, Double, Int, Double]]()
}
