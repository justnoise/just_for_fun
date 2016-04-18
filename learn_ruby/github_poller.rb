require 'httparty'
require 'json'
require 'optparse'


def get_repo_origin
	url = `git config --get remote.origin.url`.strip
	location, org_repo = url.split(':')
	org, repo = org_repo.split('/')
	p repo
	repo = repo[0..repo.size-5]
	puts "#{org} #{repo}"

	return org, repo
end


def latest_local_commit
	latest_commit = `git log | head -n 1 | awk '{print $2}'`.strip
	puts "latest local commit: #{latest_commit}"
	return latest_commit
end


def latest_remote_commit(org, repo)
	response = HTTParty.get("https://api.github.com/repos/#{org}/#{repo}/commits")
	commits = JSON.parse(response.body)
	latest_commit = ''
	if commits.size > 0
		latest_commit = commits[0]['sha']
	end
	puts "latest remote commit #{latest_commit}"
	return latest_commit
end

def pull_latest_commits
	puts "pulling latest repo"
	`git pull`
end


def parse_args
	# switch to specified branch (-b)
	usage = "Usage: #{__FILE__} [options] /path/to/local/repo"
	options = {}
	OptionParser.new do |opts|
		opts.banner = usage
		opts.on('-b', '--branch BRANCHNAME') { |v| options[:branch] = v }
	end.parse!
	if ARGV.size != 1
		puts "invalid usage"
		puts usage
		exit 1
	end
	local_repo_path = ARGV[0]
	if !File::directory?(local_repo_path)
		puts "Error: #{local_repo_path} is not a directory"
		puts usage
		exit 2
	elsif ! File::directory?(File.join(local_repo_path, '.git'))
		puts "Error: #{local_repo_path} is not a directory"
		puts usage
		exit 3
	end
	options[:local_repo_path] = local_repo_path
	return options
end


def change_branch(branch)
	puts "checking out #{branch}"
	result = `git checkout #{branch}`
end


if __FILE__ == $0
	options = parse_args
	local_repo_path = options[:local_repo_path]
	Dir.chdir(local_repo_path)
	change_branch(options[:branch] || 'master')
	org, repo = get_repo_origin
	while true
		local_commit = latest_local_commit
		remote_commit = latest_remote_commit(org, repo)
		if remote_commit != local_commit
			pull_latest_commits
		end
		puts "sleeping for a bit..."
		sleep 10
	end
end
