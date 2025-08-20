
module RefModule (
  input [7:0] din,
  output [7:0] dout
);

  assign {dout[0],dout[1],dout[2],dout[3],dout[4],dout[5],dout[6],dout[7]} = din;

endmodule

