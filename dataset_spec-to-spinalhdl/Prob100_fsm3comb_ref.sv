
module RefModule (
  input din,
  input [1:0] state,
  output reg [1:0] next_state,
  output dout
);

  parameter A=0, B=1, C=2, D=3;

  always_comb begin
    case (state)
      A: next_state = din ? B : A;
      B: next_state = din ? B : C;
      C: next_state = din ? D : A;
      D: next_state = din ? B : C;
    endcase
  end

  assign dout = (state==D);

endmodule

