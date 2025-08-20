
module RefModule (
  input din,
  input [9:0] state,
  output [9:0] next_state,
  output out1,
  output out2
);

  assign out1 = state[8] | state[9];
  assign out2 = state[7] | state[9];

  assign next_state[0] = !din && (|state[4:0] | state[7] | state[8] | state[9]);
  assign next_state[1] = din && (state[0] | state[8] | state[9]);
  assign next_state[2] = din && state[1];
  assign next_state[3] = din && state[2];
  assign next_state[4] = din && state[3];
  assign next_state[5] = din && state[4];
  assign next_state[6] = din && state[5];
  assign next_state[7] = din && (state[6] | state[7]);
  assign next_state[8] = !din && state[5];
  assign next_state[9] = !din && state[6];

endmodule

