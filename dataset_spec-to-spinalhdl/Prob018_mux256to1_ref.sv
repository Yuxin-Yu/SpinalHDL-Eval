
module RefModule (
  input [255:0] din,
  input [7:0] sel,
  output  dout
);

  assign dout = din[sel];

endmodule

