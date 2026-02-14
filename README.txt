2026-02-14: I've successfully retrieved JSON data from the tests website. It is
a matter of using the permitted user's cookies (in our case, the dpt.
supervisor). A requests session has to be created and the cookies inserted in
it before .get() is called to action. Generating an excel file from the data
obtained should be easy enough but it has to be adapted to the average user,
which means it cannot be overwhelming when it comes to the information it
displays.
