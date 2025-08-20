
module RefModule (
  input a,
  input b,
  input c,
  input d,
  input e,
  output [24:0] dout
);

  assign dout = ~{ {5{a}}, {5{b}}, {5{c}}, {5{d}}, {5{e}} } ^ {5{a,b,c,d,e}};

endmodule

