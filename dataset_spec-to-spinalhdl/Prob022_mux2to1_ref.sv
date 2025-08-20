
module RefModule (
  input a,
  input b,
  input sel,
  output dout
);

  assign dout = sel ? b : a;

endmodule

