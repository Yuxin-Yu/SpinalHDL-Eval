
module RefModule (
  input do_sub,
  input [7:0] a,
  input [7:0] b,
  output reg [7:0] dout,
  output reg result_is_zero
);

  always @(*) begin
    case (do_sub)
      0: dout = a + b;
      1: dout = a - b;
    endcase
    result_is_zero = (dout == 0);
  end

endmodule

