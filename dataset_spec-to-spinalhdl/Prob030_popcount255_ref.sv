
module RefModule (
  input [254:0] din,
  output reg [7:0] dout
);

  always_comb  begin
    dout = 0;
    for (int i=0;i<255;i++)
      dout = dout + din[i];
  end

endmodule

