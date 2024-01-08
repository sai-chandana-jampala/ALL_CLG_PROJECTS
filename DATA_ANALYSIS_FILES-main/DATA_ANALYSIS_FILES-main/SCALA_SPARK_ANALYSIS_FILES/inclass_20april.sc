/**
 * afn that takes an array and scale them and print output
 */

/**
 * write a function that takes array of int , with out using for loop and with out using map , do scaling on the aray of elements and print out
 */
def scaleArray(arr: Array[Int], scaleFactor: Int): Unit = {
  def scaleHelper(index: Int): Unit = {
    if (index < arr.length) {
      arr(index) *= scaleFactor
      scaleHelper(index + 1)
    }
  }
  scaleHelper(0)
  println(arr.mkString(", "))
}
val arr = Array(1, 2, 3, 4, 5)
scaleArray(arr, 6)

/**
 *
 */

def scaleArray(arr: Array[Int], scaleFactor: Int): Array[Int] = {
  var i = 0
  val scaledList = scala.collection.mutable.ListBuffer[Int]()

  while (i < arr.length) {
    scaledList += arr(i) * scaleFactor
    i += 1
  }

  scaledList.toArray
}

/** write a fn that find the factorial of number that takes one input  do it with for loop  */


def factorial(num: Int): Unit = {
  var result = 1
  for (i <- 1 to num) {
    result *= i
  }
  println(s"The factorial of $num is $result")
}
factorial(5)


/** now writting this in recurive way   */
/**
 * for making more value sin int we are using dig int
 * @param num
 * @return
 */
def factorial(num: Int): Int = {
  if (num == 0) 1
  else num * factorial(num - 1)
}

val result = factorial(100)
println(s"The factorial  is $result")

/**  accumlator  -- for int  */


/** by using we accu;lator we call it as tail recursion  */
/** use api fold - two paaremts one is  *
 * take an array of elements in range 1 to 1000 and get product of the elements
 */
/

