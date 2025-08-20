
module RefModule (
  input clk,
  input din,
  output logic dout
);

  initial
    dout = 0;

  always@(posedge clk) begin
    dout <= din ^ dout;
  end

endmodule

