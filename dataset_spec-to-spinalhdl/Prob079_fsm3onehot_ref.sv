
module RefModule (
  input din,
  input [3:0] state,
  output reg [3:0] next_state,
  output dout
);

  parameter A=0, B=1, C=2, D=3;

  assign next_state[A] = (state[A] | state[C]) & ~din;
  assign next_state[B] = (state[A] | state[B] | state[D]) & din;
  assign next_state[C] = (state[B] | state[D]) & ~din;
  assign next_state[D] = state[C] & din;

  assign dout = (state[D]);

endmodule

