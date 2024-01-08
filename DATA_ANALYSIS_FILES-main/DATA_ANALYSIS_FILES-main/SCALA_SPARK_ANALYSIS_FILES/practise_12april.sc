/**
 * a
 * */
def isPalindrome(lst: List[Any]): Boolean = {
  if(lst.isEmpty) true
  else lst.reverse == lst
}

val lst1 = List(1, 2, 3, 2, 1)
val lst2 = List("a", "b", "c", "b", "a")
val lst3 = List(1, 2, 3, 4)

println(isPalindrome(lst1))
println(isPalindrome(lst2))
println(isPalindrome(lst3))

/**
 * b
 */
def fib(n: Int): Int = {
  if(n == 0) 0
  else if(n == 1) 1
  else fib(n-1) + fib(n-2)
}

def sumOfEvenFibs(n: Int): Int = {
  var sum = 0
  var i = 0
  while(fib(i) <= n) {
    if(fib(i) % 2 == 0) sum += fib(i)
    i += 1
  }
  sum
}

val n = 4000000
println(sumOfEvenFibs(n))

/**
 * c
 */
def isValidEmail(email: String): Boolean = {
  val emailRegex = "^[\\w-\\.]+@([\\w-]+\\.)+[\\w-]{2,4}$".r
  emailRegex.findFirstMatchIn(email) match {
    case Some(_) => true
    case None => false
  }
}

val email1 = "john.doe@example.com"
val email2 = "jane_doe@cb.amrita.edu"
val email3 = "invalid.email@.com"

println(isValidEmail(email1))
println(isValidEmail(email2))
println(isValidEmail(email3))

/**
 * d
 */
def bitsToFlip(a: Int, b: Int): Int = {
  var xor = a ^ b
  var count = 0
  while(xor != 0) {
    count += xor & 1
    xor = xor >> 1
  }
  count
}

val a = 10
val b = 20

println(bitsToFlip(a, b)) // 4

/**
 * e
 */
  /**
def groupCharacters(str: String): Map[Int, List[Char]] = {
  str.filter(c => c.isLetter)
    .groupBy(c => str.count(_ == c))
    .mapValues(lst => lst.distinct)
}

val sentence = "Sir Percy Blakeney was an English aristocrat who risked his life to rescue French noblemen from the guillotine during the French Revolution."
val charGroups = groupCharacters(sentence)

charGroups.keys.toList.sorted.foreach { key =>
  println(s"$key: ${charGroups(key)}")
}
**/
/**
 * f
 */
def sumEvenPositions[T](arr: Seq[T]): Option[Int] = {
  val evenPositions = arr.zipWithIndex.filter(_._2 % 2 != 0).map(_._1)
  if(evenPositions.nonEmpty) Some(evenPositions.map(_.asInstanceOf[Int]).sum) else None
}

// Example usage
val array = Array(1, 2, 3, 4, 5, 6)
val list = List(1, 2, 3, 4, 5, 6, 7)
println(sumEvenPositions(array)) // Some(9)
println(sumEvenPositions(list)) // Some(9)


/**
 * g
 */
def formatPhoneNumber(phoneNumber: String): String = {
  val countryCode = "+91"
  val areaCode = phoneNumber.substring(0, 3)
  val exchange = phoneNumber.substring(3, 6)
  val station = phoneNumber.substring(6, 10)
  s"$countryCode ($areaCode) $exchange-$station"
}

// Example usage
val phoneNumber = "9445687596"
println(formatPhoneNumber(phoneNumber)) // +91 (944) 568-7596

/**
 * h
 */

def xorOperation(numbers: Seq[Int]): Int = {
  numbers.reduce(_ ^ _)
}


val array = Array(1, 2, 3, 4, 5, 6)
println(xorOperation(array))

/**
 * i
 */
def getThirdEntity(str: String): Option[(Char, Char)] = {
  val evenChars = str.zipWithIndex.filter(_._2 % 2 == 0).map(_._1)
  val oddChars = str.zipWithIndex.filter(_._2 % 2 != 0).map(_._1)
  if(evenChars.length >= 3 && oddChars.length >= 3) {
    Some((evenChars(2), oddChars(2)))
  } else {
    None
  }
}

// Example usage
val str = "abcdefg"
println(getThirdEntity(str)) // Some((d,f))

/**
 * j
 */
  /**
def calculateArea(shape: String): Double = {
  shape.toLowerCase() match {
    case "rectangle" =>
      val length = scala.io.StdIn.readLine("Enter length: ").toDouble
      val breadth = scala.io.StdIn.readLine("Enter breadth: ").toDouble
      length * breadth
    case "square" =>
      val side = scala.io.StdIn.readLine("Enter side: ").toDouble
      side * side
    case "circle" =>
      val radius = scala.io.StdIn.readLine("Enter radius: ").toDouble
      math.Pi * radius * radius
    case "parallelogram" =>
      val base = scala.io.StdIn.readLine("Enter base: ").toDouble
      val height = scala.io.StdIn.readLine("Enter height: ").toDouble
      base * height
    case "trapezoid" =>
      val base1 = scala.io.StdIn.readLine("Enter base1: ").toDouble
      val base2 = scala.io.StdIn.readLine("Enter base2: ").toDouble
      val height = scala.io.StdIn.readLine("Enter height: ").toDouble
      0.5 * (base1 + base2) * height
    case _ => throw new IllegalArgumentException(s"Invalid shape: $shape")
  }
}

// Example usage
println(calculateArea("rectangle")) // Enter length: 5, Enter breadth: 3 => 15.0
println(calculateArea("circle")) // Enter radius: 4 => 50.26548245743669
**/

/**
 * k
 */
import scala.collection.mutable
import scala.io.Source

def processResidents(filePath: String): Unit = {
  val residents = mutable.Map.empty[Int, String] // Map to store resident ID and name
  val neighbours = mutable.Map.empty[Int, Seq[String]] // Map to store neighbour ID and names
  val nonUniqueResidentIds = mutable.Set.empty[Int] // Set to store resident IDs that are not unique

  // Read from file and populate maps
  val lines = Source.fromFile(filePath).getLines()
  while (lines.hasNext) {
    val cols = lines.next().split(",").map(_.trim)
    val residentId = cols(1).toInt
    val residentName = cols(0)
    if (residents.contains(residentId)) {
      nonUniqueResidentIds += residentId
    } else {
      residents += (residentId -> residentName)
    }
    val neighbourId = cols(3).toInt
    val neighbourName = cols(2)
    if (neighbours.contains(residentId)) {
      neighbours += (residentId -> (neighbours(residentId) :+ neighbourName))
    } else {
      neighbours += (residentId -> Seq(neighbourName))
    }
  }

  // Group non-unique residents
  val nonUniqueResidents = residents.filterKeys(nonUniqueResidentIds.contains)

  // Group neighbours
  val neighbourGroups = neighbours.groupBy(_._2).mapValues(_.keys.toSeq)

  // Get group with maximum number of neighbours
  val maxNeighbours = neighbourGroups.keys.map(_.length).max
  val maxNeighbourGroup = neighbourGroups.filter(_._1.length == maxNeighbours).values

  // Print outputs
  println("Non-unique residents: " + nonUniqueResidents)
  println("Neighbour groups: " + neighbourGroups)
  println("Group(s) with maximum neighbours: " + maxNeighbourGroup)
}

// Example usage
processResidents("house data.txt")

