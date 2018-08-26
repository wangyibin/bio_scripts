#!/usr/bin/perl -w


die "Usage: perl $0 refSeq.fasta\n" if(!(defined $ARGV[0]));

print "1. tour format to agp ...\n";

my $refSeq = $ARGV[0];
my $Nseq   = "N" x 100;
my %anchordb;
my %seqdb;
open(IN, $refSeq) or die"";
$/='>';
<IN>;
while(<IN>){
	chomp;
	my ($ctg,$seq) = split(/\n/,$_,2);
	$ctg	       =~ s/\s+//g;
        $seq           =~ s/\s+//g;
	$seqdb{$ctg}   = $seq;
	}
close IN;

open(OUT, "> groups.agp") or die"";
open(SEQ, "> groups.asm.fasta") or die"";
while(my $tour = glob "*.tour"){
print "Processing $tour ...\n";
my $gid    = $tour;
   $gid    =~ s/.tour//g;
my $agp = $gid.".agp";
my $last_line = `tail -n 1 $tour`;
my @ctgdb     = split(/\s+/,$last_line);
my $a         = 0;
my $b         = 0;
my $len       = 0;
my $count     = 0;
my $fullSeq   = "";
foreach my $i(0..$#ctgdb){
	my $ctg; my $dir;
	if($ctgdb[$i]=~/(.*)([+|-])/){
		$ctg = $1; $dir = $2;
		}
	$a    = $b + 1;
        $ctg  =~ s/\s+//g;
        print "$ctg\n" if(!exists($seqdb{$ctg}));
	$len  = length $seqdb{$ctg};
	$anchordb{$ctg}++;
	$b    = $a + $len - 1;
	$count++;
	print OUT "$gid	$a	$b	$count	W	$ctg	1	$len	$dir\n";
	my $seq   = uc $seqdb{$ctg};
	if($dir eq "-"){
		$seq    = reverse $seq;
		$seq    =~ tr/ATGC/TACG/;
		}
	$fullSeq .= $seq;
	$a    = $b + 1;
	$b    = $a + 100 - 1;
	$count++;
	print OUT "$gid	$a	$b	$count	U	100	contig	yes	map\n" if($i!=$#ctgdb);
	$fullSeq .= $Nseq if($i!=$#ctgdb);
	}
print SEQ ">$gid\n$fullSeq\n";

}

foreach my $ctg (keys %seqdb){
	next if(exists($anchordb{$ctg}));
	my $len = length $seqdb{$ctg};
	print OUT "$ctg	1	$len	1	W	$ctg	1	$len	+\n";
	print SEQ ">$ctg\n$seqdb{$ctg}\n";
	}

close OUT;
close SEQ;






