/**
 * create an array stack of size "20" &  filter the prime numbers
 * greater than a random seed value less than 20 & sort the elements in descending order
 */
import scala.util.Random

val stack = Array.fill(20)(Random.nextInt(20))
  .filter(n => (2 until n).forall(i => n % i != 0) && n > Random.nextInt(20))
  .sorted(Ordering.Int.reverse)

println(stack.mkString(", "))
/**
 * create a stack of size "30" & fill in the content  with random numbers , then remove the duplicate entries
 */
import scala.util.Random
val stack = Array.fill(30)(Random.nextInt(100))
  .distinct
println(stack.mkString(", "))

/**
create 2 lists using random numbers of size 10  & etract  the common elements  from these 2 lists
 */
import scala.util.Random

val list1 = List.fill(10)(Random.nextInt(100))
val list2 = List.fill(10)(Random.nextInt(100))

val commonElements = list1.intersect(list2)

println(s"List 1: ${list1.mkString(", ")}")
println(s"List 2: ${list2.mkString(", ")}")
println(s"Common Elements: ${commonElements.mkString(", ")}")
