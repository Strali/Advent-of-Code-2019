/**
 * Code for solving day 1 of Advent of Code 2019.
 *
 * Author: Andreas Falkoven, 2019
 */

import sun.awt.im.InputMethodJFrame

import scala.annotation.tailrec
import scala.io.Source
import math.floor

object RocketFuelRequirements extends RocketFuelRequirements {
  def main(args: Array[String]): Unit = {

    def inputFile = "src/main/resources/input.txt"

    // Run fuel calculations both with and without recursion.
    val totalFuelSimple = RocketFuelRequirements.run(inputFile, runRecursive = false)
    val totalFuelRec = RocketFuelRequirements.run(inputFile, runRecursive = true)
    println("Total fuel using only original mass: " + totalFuelSimple)
    println("Total fuel when using recursion: " + totalFuelRec)
  }
}

class RocketFuelRequirements {
  /** Determines fuel requirements for list of inputs.
   *
   * @param inputFile File with list object weights for which to calculate fuel requirements.
   * @param runRecursive Boolean indicating whether simple or recursive formula should be used
   */
  def run(inputFile: String, runRecursive: Boolean): Double = {

    // Read input file into a list.
    val inputData = readFile(inputFile)

    val individualFuel = if (runRecursive) {
      // Calculate required fuel for each input recursively.
      inputData.map(recursiveFuelReq(_))
    } else {
      // Calculate required fuel for each input without recursion.
      inputData.map(simpleFuelReq(_))
    }

    // Sum all individual fuel requirements.
    val totalFuel: Double = individualFuel.sum
    totalFuel
  }

  def simpleFuelReq(mass: Double): Double = {
    /**
     * Determine fuel requirements for a given mass.
     */
    val fuelReq = (floor(mass/3) - 2)
    fuelReq
  }

  @tailrec final def recursiveFuelReq(mass: Double, accumulatedFuel: Double = 0): Double = {
    /**
     * Determine total fuel requirements, taking fuel's own weight into consideration.
     */
    // Get fuel requirement.
    val fuelReq = {
      simpleFuelReq(mass)
    }

    // Check if we should continue recursion.
    if (fuelReq > 0) {
      recursiveFuelReq(fuelReq, (accumulatedFuel + fuelReq))
    } else {
      // Return accumulated fuel.
      accumulatedFuel
    }
  }

  def readFile(filename: String): List[Int] = {
    /**
     * Read a text of input numbers into a list.
     */
    // Open and read input source into a list.
    val inputSource = Source.fromFile(filename)
    val data = (for (line <- inputSource.getLines()) yield line).toList
    inputSource.close

    // Return list elements as integers.
    data.map(_.toInt)
  }
}
