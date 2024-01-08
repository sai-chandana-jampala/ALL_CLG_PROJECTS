/**
 *  write the code in scala that  function should take any
 *  value type and it should print it
 */

def printValue(value: Any): Unit = {
  println(value)
}

/**
 * sum of elements in  number using api
 * map api , why cant we use map api and add instead we use sum ?
 * this map api alwats transforms (into colection ) and result is going to another summation
 * where as if you wanna add its just scalar value
 * instead map api u can use reduce api
 *

 *
 * write a scala code to add the each element in number using reduce api?
 **/

val numbers = List(1, 2, 3, 4, 5)
val sum = numbers.reduce((a, b) => a + b)
println(sum)

/**
 * val arr =Array(4,2,3)
 * arr.reduce(_*_)
 *
 */


/**
 * write a scala code to get maximum element from anrray using api
 */

val myArray = Array(3, 7, 1, 9, 2, 6, 8, 4, 5)

val maxElement = myArray.max

println("Maximum element in the array is: " + maxElement)


/**
 * why should we use val instead of ref or any val
 * how many sequcnes - mutable & im mutable
 * what are mutables
 * write an array as input and scale the inpit and display the output
 */



