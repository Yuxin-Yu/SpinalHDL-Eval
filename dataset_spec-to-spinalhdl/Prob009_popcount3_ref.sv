
module RefModule (
  input [2:0] din,
  output [1:0] dout
);

  assign dout = din[0]+din[1]+din[2];

endmodule

