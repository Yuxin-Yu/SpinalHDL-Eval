
module RefModule (
  input clk,
  input resetn,
  input din,
  output dout
);

  reg [3:0] sr;
  always @(posedge clk) begin
    if (~resetn)
      sr <= '0;
    else
      sr <= {sr[2:0], din};
  end

  assign dout = sr[3];

endmodule

