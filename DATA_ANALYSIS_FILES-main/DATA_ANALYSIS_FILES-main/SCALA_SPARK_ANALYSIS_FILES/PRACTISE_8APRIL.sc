/**
 * . Write a Scala program for the following
1 a. A function that takes list of Any Type and check if the list is empty,
if not check whether the given list is palindrome (do not use Palindrome API)
 */

/**
 * 1.b A function to calculate the sum of even numbers in fibonacci series
 */
def sumEvenFibonacci(limit: Int): Unit = {
  var sum = 0
  var a = 0
  var b = 1
  while (b <= limit) {
    if (b % 2 == 0) sum += b
    val c = a + b
    a = b
    b = c
  }
  println(s"The sum of even Fibonacci numbers up to $limit is $sum.")
}
sumEvenFibonacci(50)

/**
 * 1.c . A function to check valid email addresses [ex: eg: xxxxx@cb.amrita.edu or
xxxx@am.amrita.edu or xxxx@blr.amrita.edu, where x can be alphanumeric characters and
includes underscore “_”)
 */


/**
 * 1.d A function to determine the number of bits you would need to flip to convert integer A to
integer B
 */
def bitsToFlip(a: Int, b: Int): Int = (a ^ b).toBinaryString.count(_ == '1')

val a = 10
val b = 6
val numBits = bitsToFlip(a, b)
println(s"Number of bits to flip to convert $a to $b: $numBits")


/**
 * 1.e A function to group characters that are repeated same number of times from sentence
“ Sir Percy Blakeney was an English aristocrat who risked his life to rescue French
noblemen from the guillotine during the French Revolution.
 */

val sentence = "Sir Percy Blakeney was an English aristocrat who risked his life to rescue French noblemen from the guillotine during the French Revolution."

val groupedChars = sentence.filter(_.isLetter).groupBy(_.toLower).map(_.swap).groupBy(_._1).mapValues(_.unzip._2)

groupedChars.foreach { case (count, chars) => println(s"$count: ${chars.mkString}") }

/**
 * 1.fA function that can accept either array or list can return the sum of elements in the even
position
 */
def sumOfEvenPositions(arr: Seq[Int]): Int = {
  arr.zipWithIndex.filter(_._2 % 2 == 0).map(_._1).sum
}

val arr = Array(1, 5, 6, 7, 8, 9)
val result = sumOfEvenPositions(arr)
println(result)


/**
 * 1.g. A function that takes in a ten-digit number as string and prints as proper phone number
with area code, exchange, and station (ex: If input is “9445687596 -> +91 (944) 568-7596)
 */
def formatPhoneNumber(number: String): String = {
  val countryCode = "+91"
  val areaCode = number.substring(0, 3)
  val exchange = number.substring(3, 6)
  val station = number.substring(6)
  s"$countryCode ($areaCode) $exchange-$station"
}

val number = "9445687596"
val formattedNumber = formatPhoneNumber(number)
println(formattedNumber)
