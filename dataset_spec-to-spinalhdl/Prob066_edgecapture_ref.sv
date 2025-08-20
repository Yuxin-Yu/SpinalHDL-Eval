
module RefModule (
  input clk,
  input reset,
  input [31:0] din,
  output reg [31:0] dout
);

  reg [31:0] d_last;

  always @(posedge clk) begin
    d_last <= din;
    if (reset)
      dout <= '0;
    else
      dout <= dout | (~din & d_last);
  end

endmodule

