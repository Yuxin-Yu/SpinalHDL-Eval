
module RefModule (
  input a,
  input b,
  input c,
  input d,
  output dout
);

  assign dout = (~c & ~b) | (~d&~a) | (a&c&d) | (b&c&d);

endmodule

