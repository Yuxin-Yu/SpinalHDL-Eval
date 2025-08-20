
module RefModule (
  input  [99:0] din,
  output [99:0] out_both,
  output [99:0] out_any,
  output [99:0] out_different
);

  assign out_both = { 1'b0, (din[98:0] & din[99:1]) };

  assign out_any = { (din[98:0] | din[99:1]), 1'b0 };

  assign out_different = din ^ { din[0], din[99:1] };

endmodule

