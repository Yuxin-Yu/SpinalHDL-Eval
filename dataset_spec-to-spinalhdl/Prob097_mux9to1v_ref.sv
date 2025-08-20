
module RefModule (
  input [15:0] a,
  input [15:0] b,
  input [15:0] c,
  input [15:0] d,
  input [15:0] e,
  input [15:0] f,
  input [15:0] g,
  input [15:0] h,
  input [15:0] i,
  input [3:0] sel,
  output logic [15:0] dout
);

  always @(*) begin
    dout = '1;
    case (sel)
      4'h0: dout = a;
      4'h1: dout = b;
      4'h2: dout = c;
      4'h3: dout = d;
      4'h4: dout = e;
      4'h5: dout = f;
      4'h6: dout = g;
      4'h7: dout = h;
      4'h8: dout = i;
    endcase
  end

endmodule

