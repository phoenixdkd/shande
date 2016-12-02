#!/usr/bin/perl
use IO::File;

my $file = "stocklist.txt";
my $fh = IO::File->new("<$file") or die("$!");
while(my $line = $fh->getline()){
	chomp($line);
	my ($stockId, $stockName) = split(/\s+/,$line, 2);
	my $sql = "insert into stock_stock(stockid,stockname) values('$stockId', '$stockName')\;";
	print("$sql\n");
}
