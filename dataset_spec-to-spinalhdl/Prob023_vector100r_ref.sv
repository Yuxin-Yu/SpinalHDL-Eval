
module RefModule (
  input [99:0] din,
  output reg [99:0] dout
);

  always_comb
    for (int i=0;i<$bits(dout);i++)
      dout[i] = din[$bits(dout)-i-1];

endmodule

