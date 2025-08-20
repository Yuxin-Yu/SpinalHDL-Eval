
module RefModule (
  input [7:0] din,
  output parity
);

  assign parity = ^din;

endmodule

