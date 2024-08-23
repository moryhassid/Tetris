# Tetris
My tetris game


In the illustration below, we see a tetris puzzle,
with the corresponding list with the values.

at beginning the all `heights_per_width_slices` initialed to 600 each cell.

<p align="center">
  <img src="images\seq1_phase1.jpg" width="700">
</p>

We update the `heights_per_width_slices` according to the state of the tetris bricks.

<p align="center">
  <img src="images\seq1_phase2.jpg" width="700">
</p>


Using the list we can easily understand what is the maximum height in each slice.

<p align="center">
  <img src="images\seq1_phase3.jpg" width="700">
</p>


I'd like to find out what is the full row, and after finding our I should remove the complete row.
As seen in the illustration below:

<p align="center">
  <img src="images\seq1_phase4.jpg" width="700">
</p>



The are cases the row won't be filled since there are some holes, as seen in the illustration below.  
Therefore, we should make use of a grid. The grid will store the status of each brick or lack of brick. 

<p align="center">
  <img src="images\seq2_a.jpg" width="700">
</p>

Here is the content of the grid:

<p align="center">
  <img src="images\seq2_b_grid.jpg" width="700">
</p>
