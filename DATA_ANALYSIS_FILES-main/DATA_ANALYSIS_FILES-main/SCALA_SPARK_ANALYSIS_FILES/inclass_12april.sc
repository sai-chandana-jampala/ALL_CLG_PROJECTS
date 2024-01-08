/**
function that two parameters as type strings ,
check if the length of the first string is even then take first half
of the string and conctaenate with second string  in scala with 2 lines
if the length of the string is concatENATE TEH TWO STRINGS
 */
def evenconcat(x: String, y: String): String = {
  if (x.length % 2 == 0) {
    val n=x.length/2
    var x1 = ""
    for (i <- 0 to n-1) {
      x1 += x(i)
    }
    x1+y
  } else {
    x+y

  }
}
val oddop = evenconcat("hello", "world")
val evenop = evenconcat("abcd", "efgh")