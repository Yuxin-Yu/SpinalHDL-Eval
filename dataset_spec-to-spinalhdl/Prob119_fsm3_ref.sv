
module RefModule (
  input clk,
  input din,
  input areset,
  output dout
);

  parameter A=0, B=1, C=2, D=3;
  reg [1:0] state;
  reg [1:0] next;

  always_comb begin
  case (state)
    A: next = din ? B : A;
    B: next = din ? B : C;
    C: next = din ? D : A;
    D: next = din ? B : C;
  endcase
  end

  always @(posedge clk, posedge areset) begin
    if (areset) state <= A;
      else state <= next;
  end

  assign dout = (state==D);

endmodule

