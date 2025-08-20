
module RefModule (
  input in1,
  input in2,
  input in3,
  output logic dout
);

  assign dout = (~(in1 ^ in2)) ^ in3;

endmodule

