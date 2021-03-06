// This file was generated by Rapsodia (see www.mcs.anl.gov/Rapsodia)
recip = 1.0 / a.v;
r.v = log(a.v);
// scale input
s.d1_1 = 1 * a.d1_1;
s.d1_2 = 2 * a.d1_2;
s.d1_3 = 3 * a.d1_3;
s.d1_4 = 4 * a.d1_4;
s.d1_5 = 5 * a.d1_5;
s.d1_6 = 6 * a.d1_6;
s.d1_7 = 7 * a.d1_7;
s.d1_8 = 8 * a.d1_8;
s.d1_9 = 9 * a.d1_9;
s.d1_10 = 10 * a.d1_10;
// compute output
t.d1_1 = recip * (s.d1_1);
r.d1_1 = t.d1_1 / 1.0;
t.d1_2 = recip * (s.d1_2 - (t.d1_1 * a.d1_1));
r.d1_2 = t.d1_2 / 2.0;
t.d1_3 = recip * (s.d1_3 - (t.d1_1 * a.d1_2 + t.d1_2 * a.d1_1));
r.d1_3 = t.d1_3 / 3.0;
t.d1_4 = recip * (s.d1_4 - (t.d1_1 * a.d1_3 + t.d1_2 * a.d1_2 + t.d1_3 * a.d1_1));
r.d1_4 = t.d1_4 / 4.0;
t.d1_5 = recip * (s.d1_5 - (t.d1_1 * a.d1_4 + t.d1_2 * a.d1_3 + t.d1_3 * a.d1_2 + t.d1_4 * a.d1_1));
r.d1_5 = t.d1_5 / 5.0;
t.d1_6 = recip * (s.d1_6 - (t.d1_1 * a.d1_5 + t.d1_2 * a.d1_4 + t.d1_3 * a.d1_3 + t.d1_4 * a.d1_2 + t.d1_5 * a.d1_1));
r.d1_6 = t.d1_6 / 6.0;
t.d1_7 = recip * (s.d1_7 - (t.d1_1 * a.d1_6 + t.d1_2 * a.d1_5 + t.d1_3 * a.d1_4 + t.d1_4 * a.d1_3 + t.d1_5 * a.d1_2 + t.d1_6 * a.d1_1));
r.d1_7 = t.d1_7 / 7.0;
t.d1_8 = recip * (s.d1_8 - (t.d1_1 * a.d1_7 + t.d1_2 * a.d1_6 + t.d1_3 * a.d1_5 + t.d1_4 * a.d1_4 + t.d1_5 * a.d1_3 + t.d1_6 * a.d1_2 + t.d1_7 * a.d1_1));
r.d1_8 = t.d1_8 / 8.0;
t.d1_9 = recip * (s.d1_9 - (t.d1_1 * a.d1_8 + t.d1_2 * a.d1_7 + t.d1_3 * a.d1_6 + t.d1_4 * a.d1_5 + t.d1_5 * a.d1_4 + t.d1_6 * a.d1_3 + t.d1_7 * a.d1_2 + t.d1_8 * a.d1_1));
r.d1_9 = t.d1_9 / 9.0;
t.d1_10 = recip * (s.d1_10 - (t.d1_1 * a.d1_9 + t.d1_2 * a.d1_8 + t.d1_3 * a.d1_7 + t.d1_4 * a.d1_6 + t.d1_5 * a.d1_5 + t.d1_6 * a.d1_4 + t.d1_7 * a.d1_3 + t.d1_8 * a.d1_2 + t.d1_9 * a.d1_1));
r.d1_10 = t.d1_10 / 10.0;
// scale input
s.d2_1 = 1 * a.d2_1;
s.d2_2 = 2 * a.d2_2;
s.d2_3 = 3 * a.d2_3;
s.d2_4 = 4 * a.d2_4;
s.d2_5 = 5 * a.d2_5;
s.d2_6 = 6 * a.d2_6;
s.d2_7 = 7 * a.d2_7;
s.d2_8 = 8 * a.d2_8;
s.d2_9 = 9 * a.d2_9;
s.d2_10 = 10 * a.d2_10;
// compute output
t.d2_1 = recip * (s.d2_1);
r.d2_1 = t.d2_1 / 1.0;
t.d2_2 = recip * (s.d2_2 - (t.d2_1 * a.d2_1));
r.d2_2 = t.d2_2 / 2.0;
t.d2_3 = recip * (s.d2_3 - (t.d2_1 * a.d2_2 + t.d2_2 * a.d2_1));
r.d2_3 = t.d2_3 / 3.0;
t.d2_4 = recip * (s.d2_4 - (t.d2_1 * a.d2_3 + t.d2_2 * a.d2_2 + t.d2_3 * a.d2_1));
r.d2_4 = t.d2_4 / 4.0;
t.d2_5 = recip * (s.d2_5 - (t.d2_1 * a.d2_4 + t.d2_2 * a.d2_3 + t.d2_3 * a.d2_2 + t.d2_4 * a.d2_1));
r.d2_5 = t.d2_5 / 5.0;
t.d2_6 = recip * (s.d2_6 - (t.d2_1 * a.d2_5 + t.d2_2 * a.d2_4 + t.d2_3 * a.d2_3 + t.d2_4 * a.d2_2 + t.d2_5 * a.d2_1));
r.d2_6 = t.d2_6 / 6.0;
t.d2_7 = recip * (s.d2_7 - (t.d2_1 * a.d2_6 + t.d2_2 * a.d2_5 + t.d2_3 * a.d2_4 + t.d2_4 * a.d2_3 + t.d2_5 * a.d2_2 + t.d2_6 * a.d2_1));
r.d2_7 = t.d2_7 / 7.0;
t.d2_8 = recip * (s.d2_8 - (t.d2_1 * a.d2_7 + t.d2_2 * a.d2_6 + t.d2_3 * a.d2_5 + t.d2_4 * a.d2_4 + t.d2_5 * a.d2_3 + t.d2_6 * a.d2_2 + t.d2_7 * a.d2_1));
r.d2_8 = t.d2_8 / 8.0;
t.d2_9 = recip * (s.d2_9 - (t.d2_1 * a.d2_8 + t.d2_2 * a.d2_7 + t.d2_3 * a.d2_6 + t.d2_4 * a.d2_5 + t.d2_5 * a.d2_4 + t.d2_6 * a.d2_3 + t.d2_7 * a.d2_2 + t.d2_8 * a.d2_1));
r.d2_9 = t.d2_9 / 9.0;
t.d2_10 = recip * (s.d2_10 - (t.d2_1 * a.d2_9 + t.d2_2 * a.d2_8 + t.d2_3 * a.d2_7 + t.d2_4 * a.d2_6 + t.d2_5 * a.d2_5 + t.d2_6 * a.d2_4 + t.d2_7 * a.d2_3 + t.d2_8 * a.d2_2 + t.d2_9 * a.d2_1));
r.d2_10 = t.d2_10 / 10.0;
// scale input
s.d3_1 = 1 * a.d3_1;
s.d3_2 = 2 * a.d3_2;
s.d3_3 = 3 * a.d3_3;
s.d3_4 = 4 * a.d3_4;
s.d3_5 = 5 * a.d3_5;
s.d3_6 = 6 * a.d3_6;
s.d3_7 = 7 * a.d3_7;
s.d3_8 = 8 * a.d3_8;
s.d3_9 = 9 * a.d3_9;
s.d3_10 = 10 * a.d3_10;
// compute output
t.d3_1 = recip * (s.d3_1);
r.d3_1 = t.d3_1 / 1.0;
t.d3_2 = recip * (s.d3_2 - (t.d3_1 * a.d3_1));
r.d3_2 = t.d3_2 / 2.0;
t.d3_3 = recip * (s.d3_3 - (t.d3_1 * a.d3_2 + t.d3_2 * a.d3_1));
r.d3_3 = t.d3_3 / 3.0;
t.d3_4 = recip * (s.d3_4 - (t.d3_1 * a.d3_3 + t.d3_2 * a.d3_2 + t.d3_3 * a.d3_1));
r.d3_4 = t.d3_4 / 4.0;
t.d3_5 = recip * (s.d3_5 - (t.d3_1 * a.d3_4 + t.d3_2 * a.d3_3 + t.d3_3 * a.d3_2 + t.d3_4 * a.d3_1));
r.d3_5 = t.d3_5 / 5.0;
t.d3_6 = recip * (s.d3_6 - (t.d3_1 * a.d3_5 + t.d3_2 * a.d3_4 + t.d3_3 * a.d3_3 + t.d3_4 * a.d3_2 + t.d3_5 * a.d3_1));
r.d3_6 = t.d3_6 / 6.0;
t.d3_7 = recip * (s.d3_7 - (t.d3_1 * a.d3_6 + t.d3_2 * a.d3_5 + t.d3_3 * a.d3_4 + t.d3_4 * a.d3_3 + t.d3_5 * a.d3_2 + t.d3_6 * a.d3_1));
r.d3_7 = t.d3_7 / 7.0;
t.d3_8 = recip * (s.d3_8 - (t.d3_1 * a.d3_7 + t.d3_2 * a.d3_6 + t.d3_3 * a.d3_5 + t.d3_4 * a.d3_4 + t.d3_5 * a.d3_3 + t.d3_6 * a.d3_2 + t.d3_7 * a.d3_1));
r.d3_8 = t.d3_8 / 8.0;
t.d3_9 = recip * (s.d3_9 - (t.d3_1 * a.d3_8 + t.d3_2 * a.d3_7 + t.d3_3 * a.d3_6 + t.d3_4 * a.d3_5 + t.d3_5 * a.d3_4 + t.d3_6 * a.d3_3 + t.d3_7 * a.d3_2 + t.d3_8 * a.d3_1));
r.d3_9 = t.d3_9 / 9.0;
t.d3_10 = recip * (s.d3_10 - (t.d3_1 * a.d3_9 + t.d3_2 * a.d3_8 + t.d3_3 * a.d3_7 + t.d3_4 * a.d3_6 + t.d3_5 * a.d3_5 + t.d3_6 * a.d3_4 + t.d3_7 * a.d3_3 + t.d3_8 * a.d3_2 + t.d3_9 * a.d3_1));
r.d3_10 = t.d3_10 / 10.0;
