
module RefModule (
  input a,
  input b,
  output dout
);

  assign dout = ~(a | b);

endmodule

