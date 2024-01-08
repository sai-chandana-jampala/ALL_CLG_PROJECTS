/**a. to check if the value of the first or last element of
  a given array(length more than 5) are same or not.
 */
val arr = Array(1, 2, 3, 4, 5, 1)
if (arr.head == arr.last) println("The first and last elements are the same.")
else println("The first and last elements are different.")

/**
 * b. Reverse the array (do not use APIs)
 */

val arr = Array(1, 2, 3, 4, 5)
val reversedArr = for (i <- arr.length - 1 to 0 by -1) yield arr(i)
println(reversedArr.mkString(", "))


/**
 * c. Get the sum of prime numbers and even numbers in array
 */
val arr = Array(1, 2, 3, 4, 5, 6, 7, 8, 9)

val primes = arr.filter(num => (2 to Math.sqrt(num).toInt).forall(num % _ != 0))
val sumPrimes = primes.sum

val evens = arr.filter(_ % 2 == 0)
val sumEvens = evens.sum

println(s"Sum of primes: $sumPrimes")
println(s"Sum of evens: $sumEvens")

/**
 * d. Find first three smallest elements in the array
 */

val arr = Array(5, 2, 7, 1, 8, 3, 9, 4, 6)
val firstThreeSmallest = arr.sorted.take(3)
println(s"The first three smallest elements are: ${firstThreeSmallest.mkString(", ")}")

/**
 * e. Print the characters that are repeated more than twice from the given string
 */
val str = "sai chandana"
val counts = Array.fill(256)(0)
for (c <- str) counts(c) += 1
for (c <- str if counts(c) > 2) println(c)


/**
 * f. Transpose the given matrix and find the diagonal sum
 */

val matrix = Array.ofDim[Int](3, 3)
matrix(0) = Array(1, 2, 3)
matrix(1) = Array(4, 5, 6)
matrix(2) = Array(7, 8, 9)

val transposedMatrix = matrix.transpose
var diagonalSum = 0
for (i <- 0 until transposedMatrix.length) {
  diagonalSum += transposedMatrix(i)(i)
}

println(s"Transposed matrix: ${transposedMatrix.map(_.mkString(" ")).mkString("\n")}")
println(s"Diagonal sum: $diagonalSum")


/**
 *  1st practise problems
 */

/**
 * write the code in the functional way
 */