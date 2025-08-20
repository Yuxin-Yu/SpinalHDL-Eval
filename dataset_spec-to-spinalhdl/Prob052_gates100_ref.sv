
module RefModule (
  input [99:0] din,
  output out_and,
  output out_or,
  output out_xor
);

  assign out_and = &din;
  assign out_or = |din;
  assign out_xor = ^din;

endmodule

