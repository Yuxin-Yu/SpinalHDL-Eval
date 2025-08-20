
module RefModule (
  input sel,
  input [7:0] a,
  input [7:0] b,
  output reg [7:0] dout
);

  // assign dout = (~sel & a) | (sel & b);
  assign dout = sel ? a : b;

endmodule

