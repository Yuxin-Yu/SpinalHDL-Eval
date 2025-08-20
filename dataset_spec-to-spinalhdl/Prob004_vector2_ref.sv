
module RefModule (
  input [31:0] din,
  output [31:0] dout
);

  assign dout = {din[7:0], din[15:8], din[23:16], din[31:24]};

endmodule

