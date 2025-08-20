
module RefModule (
  input [2:0] sel,
  input [3:0] data0,
  input [3:0] data1,
  input [3:0] data2,
  input [3:0] data3,
  input [3:0] data4,
  input [3:0] data5,
  output reg [3:0] dout
);

  always @(*) begin
    case (sel)
      3'h0: dout = data0;
      3'h1: dout = data1;
      3'h2: dout = data2;
      3'h3: dout = data3;
      3'h4: dout = data4;
      3'h5: dout = data5;
      default: dout = 4'b0;
    endcase
  end

endmodule

