
module RefModule (
  input in1,
  input in2,
  output logic dout
);

  assign dout = ~(in1 | in2);

endmodule

