use strict;
use warnings;

##read in sorted bam file name from directory
#

my @files = glob("*_sorted.bam");

#
##S522W_1B.sorted.bam

foreach my $file (@files) {
        #split at '.'
        my $prefix = (split/\./, $file)[0];
        my $scriptfile = $prefix . '.bash';

my $heredoc = <<"DOC";

##filter to keep only first read in pair; convert to bam keeping only reads that were members of proper pairs.
samtools view -h -f 0x0040 $file | samtools view -bS -f 0x0002 - > $prefix.properReads1.bam

##filter to retain only reads mapping to the minus strand
samtools view -bh -f 0x10 $prefix.properReads1.bam > $prefix.R1_minus.bam

##filter to retain only reads NOT mapping to the minus strand
samtools view -bh -F 0x10 $prefix.properReads1.bam > $prefix.R1_plus.bam

samtools index $prefix.R1_plus.bam
samtools index $prefix.R1_minus.bam
DOC

        open my($fh), ">$scriptfile";
        print $fh $heredoc;
        close($fh);
}


exit;