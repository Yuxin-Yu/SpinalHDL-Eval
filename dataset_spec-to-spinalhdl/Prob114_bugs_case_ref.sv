
module RefModule (
  input [7:0] code,
  output reg [3:0] dout,
  output reg valid
);

  // uhh.. make a case statement: maps scancode to 0-9, but accidentally
  // infer a latch? and have one of the entries be wrong? (duplicate
  // case, using different base!)

  always @(*) begin
    dout = 0;
    valid = 1;
    case (code)
      8'h45: dout = 0;
      8'h16: dout = 1;
      8'h1e: dout = 2;
      8'h26: dout = 3;
      8'h25: dout = 4;
      8'h2e: dout = 5;
      8'h36: dout = 6;
      8'h3d: dout = 7;
      8'h3e: dout = 8;
      8'h46: dout = 9;
      default: valid = 0;
    endcase
  end

endmodule

