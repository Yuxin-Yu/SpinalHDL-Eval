
module RefModule (
  input a,
  input b,
  input c,
  input d,
  output reg dout
);

  always @(*) begin
    case({a,b,c,d})
      4'h0: dout = 0;
      4'h1: dout = 1;
      4'h3: dout = 0;
      4'h2: dout = 1;
      4'h4: dout = 1;
      4'h5: dout = 0;
      4'h7: dout = 1;
      4'h6: dout = 0;
      4'hc: dout = 0;
      4'hd: dout = 1;
      4'hf: dout = 0;
      4'he: dout = 1;
      4'h8: dout = 1;
      4'h9: dout = 0;
      4'hb: dout = 1;
      4'ha: dout = 0;
    endcase
  end

endmodule

