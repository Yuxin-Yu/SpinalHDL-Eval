
module RefModule (
  input [7:0] din,
  output [31:0] dout
);

  assign dout = { {24{din[7]}}, din };

endmodule

