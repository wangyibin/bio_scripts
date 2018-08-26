#!/usr/bin/perl -w

die"Usage: perl $0 hic_result/ sample chrname\n" if(!defined $ARGV[0] or !defined $ARGV[1] or !defined $ARGV[2]);
my @resdb = qw /20k 40k 150k 500k 1M/;
#my @resdb = qw /40k 150k 500k/;
my $hic_result = $ARGV[0];
my $sample     = $ARGV[1];
my $chrn       = $ARGV[2];
foreach my $res(@resdb){
	my $lab  = $res."out";
	my $resD = 0;
	if($res=~/20k/){
		$resD = 20000;
	}elsif($res=~/40k/){
		$resD = 40000;
	}elsif($res=~/150k/){
		$resD = 150000;
	}elsif($res=~/500k/){
		$resD = 500000;
	}elsif($res=~/1M/){
		$resD = 1000000;
		}

	my $cmd = "python ~/software/HiCPlotter/HiCPlotter.py -ext pdf -f ".$hic_result."/matrix/".$sample."/iced/".$resD."/".$sample."_".$resD."_iced.matrix ";
	   $cmd.= "-o ".$lab." -r ".$resD." -tri 1 -bed ".$hic_result."/matrix/".$sample."/raw/".$resD."/".$sample."_".$resD."_ord.bed -n ".$chrn."_".$res."Res -chr ".$chrn;
	print "$cmd\n";
#	system($cmd);
	}
