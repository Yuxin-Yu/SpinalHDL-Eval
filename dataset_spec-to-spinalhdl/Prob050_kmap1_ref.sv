
module RefModule (
  input a,
  input b,
  input c,
  output dout
);

  assign dout = (a | b | c);

endmodule

