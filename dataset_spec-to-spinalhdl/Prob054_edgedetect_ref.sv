
module RefModule (
  input clk,
  input [7:0] din,
  output reg [7:0] pedge
);

  reg [7:0] d_last;

  always @(posedge clk) begin
    d_last <= din;
    pedge <= din & ~d_last;
  end

endmodule

