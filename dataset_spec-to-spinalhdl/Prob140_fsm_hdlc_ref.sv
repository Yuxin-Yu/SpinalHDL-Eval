
module RefModule (
  input clk,
  input reset,
  input din,
  output disc,
  output flag,
  output err
);

  parameter [3:0] S0=0, S1=1, S2=2, S3=3, S4=4, S5=5, S6=6, SERR=7, SDISC=8, SFLAG=9;
  reg [3:0] state, next;

  assign disc = state == SDISC;
  assign flag = state == SFLAG;
  assign err = state == SERR;

  always @(posedge clk) begin
    case (state)
      S0: state <= din ? S1 : S0;
      S1: state <= din ? S2 : S0;
      S2: state <= din ? S3 : S0;
      S3: state <= din ? S4 : S0;
      S4: state <= din ? S5 : S0;
      S5: state <= din ? S6 : SDISC;
      S6: state <= din ? SERR : SFLAG;
      SERR: state <= din ? SERR : S0;
      SFLAG: state <= din ? S1 : S0;
      SDISC: state <= din ? S1 : S0;
      default: state <= 'x;
    endcase

    if (reset) state <= S0;
  end

endmodule

