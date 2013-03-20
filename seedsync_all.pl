#!/usr/bin/perl -w

#SeedSync, a utility to identify motifs (miRNA seeds) occuring in the same UTR.
#syntax: seedsync.pl <FASTA sequence file> <FASTA mature miRNAs>

#MAKE SURE MOTIFS ARE IN ALL CAPS!

{   use Bio::SeqIO;
    use Math::Combinatorics;
    use Parallel::ForkManager;
	use List::MoreUtils qw(uniq);
	#use Statistics::Descriptive;
	use Time::HiRes qw(gettimeofday tv_interval); #get better than 1 second resolution
    
    $MAX_PROCESSES=1; #probably don't want this to be greater than the # of cores you have.
    
    #generate array of all possible miRNA seed combinations
    print "opening miRNA FASTA file...";
    $mirs = Bio::SeqIO->new(-file => "$ARGV[1]", -format => 'fasta');
    print "ok.\n";
    
    $record;
    @hsa_mir_SEQ;
	@hsa_mir_SEQ_temp;
    
    #slice out human seed sequences (bases 2-7)
    print "Pull out bases 2-n of miRNA sequence...";
    while( $record = $mirs->next_seq() ) {
        
        $seq=$record->seq;
        $id=$record->id;
        
        if($id =~ /hsa/) {
            $seed = substr $seq, 1, 7;
            #print "$seed\n";
           push(@hsa_mir_SEQ_temp, $seed);
        }
    }
    print "ok.\n Filtering duplicate seeds...\n";
	
	@hsa_mir_SEQ = uniq @hsa_mir_SEQ_temp;
	undef @hsa_mir_SEQ_temp;
    
    #array of all possible combinations    
    print "generating all possible combinations...\n";
    @combi = combine(2, @hsa_mir_SEQ);
    print "\n$#combi generated, let's clean out identical pairs...\n";
    undef @hsa_mir_SEQ;
	
    #this will leave motif pairs that are identical n-mers. Weed these out!
    
    for $p (0 .. $#combi){
        if("$combi[$p][0]" ne "$combi[$p][1]"){
            @goodPair=($combi[$p][0],$combi[$p][1]);
            #print "$goodPair[0], $goodPair[1]\n";
            push(@combinations, [@goodPair]);
        }
        
    }
    
    undef @combi;
    
    print "\n$#combinations pairs remain.";

    #parse 3' UTR FASTA file
    
    $u;
    @recs;
    $utr_file = Bio::SeqIO->new(-file => "$ARGV[0]", -format => 'fasta' -alphabet => 'dna');
    while( $u = $utr_file->next_seq() ){
        $string=$u->seq;
        push(@recs,$string);
    }
    undef $utr_file;
    $pm = new Parallel::ForkManager($MAX_PROCESSES);
    
    open(OUTFILE, ">seedpairs_numhits.test.txt");
    print OUTFILE "Motif 1\tMotif 2\tCount\n";
    
    #for $i (0 .. $#combinations){
     $tloop0 = [gettimeofday];
	 for $i (0 .. 100){   
        # Forks and returns the pid for the child:
        
        $pm->start and next; # do the fork
        
		#Time each loop.
		$t0 = [gettimeofday];
		
        $motif1 = $combinations[$i][0];
        $motif2 = $combinations[$i][1];
    
        $count=0;
        
        print "processing motifs: $motif1\t$motif2\t";
        for $j ( 0 .. $#recs ) {
            
            $string = $recs[$j];
            #search for both motifs in one UTR
            if($string =~ /$motif1/ && $string =~ /$motif2/){
                $count++;
            }
        }

        #list stats
		$t1 = [gettimeofday];
        print "$count\t";
		print tv_interval($t0,$t1);
		print "\n";
        print OUTFILE "$motif1\t$motif2\t$count\n";

        $pm->finish; # Terminates the child process
        }
    $pm->wait_all_children;
	
	$tloop1 = [gettimeofday];
	$looptime = tv_interval($tloop0,$tloop1);
    print "Total Loop time: $looptime\n";
	
	
    close OUTFILE;
    print "\nDone!\n";
}
