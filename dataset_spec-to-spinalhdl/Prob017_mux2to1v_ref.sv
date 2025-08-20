
module RefModule (
  input [99:0] a,
  input [99:0] b,
  input sel,
  output [99:0] dout
);

  assign dout = sel ? b : a;

endmodule

