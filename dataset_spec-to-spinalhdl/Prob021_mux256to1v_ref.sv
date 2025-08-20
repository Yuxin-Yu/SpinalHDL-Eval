
module RefModule (
  input [1023:0] din,
  input [7:0] sel,
  output [3:0] dout
);

  assign dout = {din[sel*4+3], din[sel*4+2], din[sel*4+1], din[sel*4+0]};

endmodule

