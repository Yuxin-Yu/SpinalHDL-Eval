
module RefModule (
  input clk,
  input din,
  input areset,
  output dout
);

  parameter A=0, B=1;
  reg state;
  reg next;

    always_comb begin
    case (state)
      A: next = din ? A : B;
      B: next = din ? B : A;
    endcase
    end

    always @(posedge clk, posedge areset) begin
    if (areset) state <= B;
        else state <= next;
  end

  assign dout = (state==B);

endmodule

